// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract OttomanCollection is ERC721URIStorage, ERC721Holder, Ownable {
    uint256 public tokenCounter;
    IERC20 public ottomanToken;

    bool public creating = true;

    uint256 public constant costInOTT = 5000 * 10**18;
    bool public purchasing = false;

    string[] public sultans = [
        "osman_i",
        "orhan",
        "murad_i",
        "bayezid_i",
        "mehmed_i",
        "murad_ii"
    ];
    uint256 public numberOfSultans = sultans.length;

    constructor(address _ottomanToken)
        public
        ERC721("OttomanCollection", "OTTC")
    {
        tokenCounter = 0;
        ottomanToken = IERC20(_ottomanToken);
    }

    function getSmartContractBalance() public view returns (uint256) {
        return ottomanToken.balanceOf(address(this));
    }

    function createCollectible(string memory tokenURI) public onlyOwner {
        require(creating == true, "Tokens can no longer be created!");
        uint256 newTokenId = tokenCounter;
        _safeMint(address(this), newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
        if (tokenCounter == 6) {
            purchasing = true;
            creating = false;
        }
    }

    function purchaseCollectible(uint256 _tokenId) external {
        require(
            purchasing == true,
            "Tokens are not yet available for purchase!"
        );
        require(
            _exists(_tokenId) != false,
            "The collectible with this id does not exist!"
        );
        require(
            ownerOf(_tokenId) == address(this),
            "This collectible has already purchased!"
        );
        require(
            ottomanToken.balanceOf(msg.sender) >= costInOTT,
            "Not enough OTT to purchase a collectible!"
        );
        bool success = ottomanToken.transferFrom(msg.sender, address(this), costInOTT);
        if (success == true) {
            _safeTransfer(address(this), msg.sender, _tokenId, "");
        }
    }
    function withdrawTokens() public onlyOwner {
        uint256 contractBalance = ottomanToken.balanceOf(address(this));
        ottomanToken.transfer(msg.sender, contractBalance);
    }
}
